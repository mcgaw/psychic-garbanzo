# python3

class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == 'add':
            self.name = query[2]

def read_queries():
    n = int(input())
    return [Query(input().split()) for i in range(n)]

def write_responses(result):
    print('\n'.join(result))

def process_queries(queries):
    result = []
    # Keep list of all existing (i.e. not deleted yet) contacts.
    contacts = [None for x in range (0, 10000000)]
    for cur_query in queries:
        if cur_query.type == 'add':
            # if we already have contact with such number,
            # we should rewrite contact's name
            contacts[int(cur_query.number)] = cur_query
        elif cur_query.type == 'del':
            contacts[int(cur_query.number)] = None
        else:
            response = 'not found'
            contact = contacts[int(cur_query.number)]
            if contact is None:
                response = 'not found'
            else:
                response = contact.name
            result.append(response)
    return result

if __name__ == '__main__':
    write_responses(process_queries(read_queries()))

