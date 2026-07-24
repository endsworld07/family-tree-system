from models.connection import Connection


class ConnectionEngine:

    def build(self, nodes):

        node_map = {}

        for node in nodes:
            node_map[node.relationship.title] = node

        connections = []

        def connect(from_title, to_title):

            if (
                from_title in node_map
                and to_title in node_map
            ):
                connections.append(
                    Connection(
                        from_node=node_map[from_title],
                        to_node=node_map[to_title],
                    )
                )

        connect("FATHER", "SELF")
        connect("MOTHER", "SELF")
        connect("SELF", "SPOUSE")
        connect("SELF", "CHILD")

        return connections