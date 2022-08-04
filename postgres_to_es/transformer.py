

class Transformer:

    def transform(self, query):
        es_data = []
        for row in query:
            for i in row:
                if row[i] is None:
                    row[i] = []
            es_data.append(
                {
                    "create": {"_index": "movies", "_id": row['id']}
                }
            )
            es_data.append(row)
        return es_data
            