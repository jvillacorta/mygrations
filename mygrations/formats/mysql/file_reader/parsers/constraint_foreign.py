from mygrations.core.parse.parser import parser

class constraint_foreign( parser ):

    definition_type = 'constraint'

    name = ''
    column = ''
    foreign_table = ''
    foreign_column = ''
    on_update = ''
    on_delete = ''
    has_comma = False

    # CONSTRAINT `accounts_status_id_ref_account_statuses_id` FOREIGN KEY (`status_id`) REFERENCES `account_statuses` (`id`) ON UPDATE CASCADE
    rules = [
        { 'type': 'literal', 'value': 'CONSTRAINT' },
        { 'type': 'regexp', 'name': 'name', 'value': '[^\(\s\)]+' },
        { 'type': 'literal', 'value': 'FOREIGN KEY (' },
        { 'type': 'regexp', 'name': 'column', 'value': '[^\(\s\)]+' },
        { 'type': 'literal', 'value': ') REFERENCES' },
        { 'type': 'regexp', 'name': 'foreign_table', 'value': '[^\(]+' },
        { 'type': 'literal', 'value': '(' },
        { 'type': 'regexp', 'name': 'foreign_column', 'value': '[^\)]+' },
        { 'type': 'literal', 'value': ')' },
        { 'type': 'literal', 'value': 'ON DELETE CASCADE', 'optional': True },
        { 'type': 'literal', 'value': 'ON DELETE NO ACTION', 'optional': True },
        { 'type': 'literal', 'value': 'ON DELETE RESTRICT', 'optional': True },
        { 'type': 'literal', 'value': 'ON DELETE SET DEFAULT', 'optional': True },
        { 'type': 'literal', 'value': 'ON DELETE SET NULL', 'optional': True },
        { 'type': 'literal', 'value': 'ON UPDATE CASCADE', 'optional': True },
        { 'type': 'literal', 'value': 'ON UPDATE NO ACTION', 'optional': True },
        { 'type': 'literal', 'value': 'ON UPDATE RESTRICT', 'optional': True },
        { 'type': 'literal', 'value': 'ON UPDATE SET DEFAULT', 'optional': True },
        { 'type': 'literal', 'value': 'ON UPDATE SET NULL', 'optional': True },
        { 'type': 'literal', 'value': ',', 'optional': True, 'name': 'ending_comma' }
    ]

    process( self ):

        self.name = self._values['name']
        self.column = self._values['column']
        self.foreign_table = self._values['foreign_table']
        self.foreign_column = self._values['foreign_column']

        # figure out what our rules are
        self.on_delete = self.find_action( 'DELETE' )
        self.on_update = self.find_action( 'UPDATE' )

        self.has_comma = True if 'ending_comma' in self._values else False

    def find_action( self, update_type ):

        # watch for more than one action for this type
        found = ''
        for action in [ 'CASCADE', 'NO ACTION', 'RESTRICT', 'SET DEFAULT', 'SET NULL' ]:
            if not ( 'ON %s %s' % update_type, action ) in self._values:
                continue

            if found:
                self.errors.append( 'Found contradictory rules in foreign constraint for ON %s' % update_type )
            else:
                found = action

        return found
