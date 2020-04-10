import psycopg2
import psycopg2.extras
import psycopg2.sql


class DatabaseError(Exception):
    pass


class NotFoundError(Exception):
    pass


class Entity(object):
    db = psycopg2.connect("dbname=orm_base user=postgres password=postgres host=localhost")  # None

    # ORM part 1
    __delete_query    = 'DELETE FROM "{table}" WHERE {table}_id=%s'
    __insert_query    = 'INSERT INTO "{table}" ({columns}) VALUES ({placeholders}) RETURNING "{table}_id"'
    __list_query      = 'SELECT * FROM "{table}"'
    __select_query    = 'SELECT * FROM "{table}" WHERE {table}_id=%s'
    __update_query    = 'UPDATE "{table}" SET {columns} WHERE {table}_id=%s'

    # ORM part 2
    __parent_query    = 'SELECT * FROM "{table}" WHERE {parent}_id=%s'
    __sibling_query   = 'SELECT * FROM "{sibling}" NATURAL JOIN "{join_table}" WHERE {table}_id=%s'
    __update_children = 'UPDATE "{table}" SET {parent}_id=%s WHERE {table}_id IN ({children})'

    def __init__(self, id=None):
        if self.__class__.db is None:
            raise DatabaseError()

        self.__cursor   = self.__class__.db.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        self.__fields   = {}
        self.__id       = id
        self.__loaded   = False
        self.__modified = False
        self.__table    = self.__class__.__name__.lower()

        if id:
            self.__load()
        # else:
        #     for field in self._columns:
        #         self.__fields[field] = None
        #         self.__fields['created'] = None
        #         self.__fields['updated'] = None

    def __getattr__(self, name):
        # check, if instance is modified and throw an exception
        # get corresponding data from database if needed
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    getter with name as an argument
        # throw an exception, if attribute is unrecognized
        if self.__modified:
            raise DatabaseError()
        else:
            if not self.__loaded:
                self.__load()

            if self.__table + '_' + name in self.__fields:
                return self.__fields[self.__table + '_' + name]
            else:
                raise NotFoundError()

    def __setattr__(self, name, value):
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    setter with name and value as arguments or use default implementation

        if name in self._columns:
            self.__fields[self.__table + '_' + name] = value
            self.__modified = True
        else:
            object.__setattr__(self, name, value)

    def __execute_query(self, query, args):
        # execute an sql statement and handle exceptions together with transactions
        self.__cursor.execute(query, args)
        # TODO: handle exceptions

    def __insert(self):
        # generate an insert query string from fields keys and values and execute it
        # use prepared statements
        # save an insert id
        self.__execute_query(self.__insert_query.format(
            table=self.__table,
            columns=", ".join(self._columns),
            placeholders=", ".join([self.__fields[self.__table + '_' + i] for i in self._columns])
            )
        )
        self.__id = self.__cursor.fetchone()
        # TODO: Remove debug
        print(self.id)

    def __load(self):
        # if current instance is not loaded yet — execute select statement
        # and store it's result as an associative array (fields), where column names used as keys
        # TODO: DEBUG
        print('load')

        if not self.__loaded:
            self.__cursor.execute(self.__select_query.format(table=self.__table), (self.__id,))

            res = self.__cursor.fetchone()
            for field, value in zip(self._columns, res[1:]):
                self.__fields[self.__table + '_' + field] = value

            self.__fields[self.__table + '_created'] = res[-2]
            self.__fields[self.__table + '_updated'] = res[-1]
            self.__loaded = True

    def __update(self):
        # generate an update query string from fields keys and values and execute it
        # use prepared statements
        query = self.__update_query.format(
            table=self.__table,
            columns=', '.join(self.__table + '_' + k + '=' + '%s' for k in self._columns)
        )
        self.__execute_query(query, (*(self.__fields[self.__table + '_' + x] for x in self._columns), self.id))

    def _get_children(self, name):
        # return an array of child entity instances
        # each child instance must have an id and be filled with data
        pass

    def _get_column(self, name):
        # return value from fields array by <table>_<name> as a key
        return self.__fields[self.__table + '_' + name]

    def _get_parent(self, name):
        # ORM part 2
        # get parent id from fields with <name>_id as a key
        # return an instance of parent entity class with an appropriate id
        pass

    def _get_siblings(self, name):
        # ORM part 2
        # get parent id from fields with <name>_id as a key
        # return an array of sibling entity instances
        # each sibling instance must have an id and be filled with data
        pass

    def _set_column(self, name, value):
        # put new value into fields array with <table>_<name> as a key
        pass

    def _set_parent(self, name, value):
        # ORM part 2
        # put new value into fields array with <name>_id as a key
        # value can be a number or an instance of Entity subclass
        pass

    @classmethod
    def all(cls):
        # get ALL rows with ALL columns from corrensponding table
        # for each row create an instance of appropriate class
        # each instance must be filled with column data, a correct id and MUST NOT query a database for own fields any more
        # return an array of instances
        pass

    def delete(self):
        # execute delete query with appropriate id
        pass

    @property
    def id(self):
        # try to guess yourself
        return self.__id

    @property
    def created(self):
        # try to guess yourself
        return self.__fields[self.__table + '_created']

    @property
    def updated(self):
        # try to guess yourself
        return self.__fields[self.__table + '_updated']

    def save(self):
        if self.id:
            self.__update()
            self.__modified = False
        else:
            self.__insert()
            # TODO: maybe rework
            self.__loaded = True
