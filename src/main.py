from query import ask

print()
print("=" * 50)
print("Document Q&A Bot")
print("Type 'exit' to quit")
print("=" * 50)
print()

while True:
    q = input("Ask: ")

    if q.lower() == "exit":
        break

    try:
        answer, sources = ask(q)

        print()
        print("Answer:")
        print(answer)

        print()
        print("Sources:")

        seen = set()

        for item in sources:
            key = (
                item["source"],
                item["page"]
            )

            if key not in seen:
                seen.add(key)

                print(
                    f"- {item['source']} "
                    f"(Page {item['page']})"
                )

    except Exception as e:
        print()
        print("Error:", e)

    print()
    print("-" * 50)
    print()