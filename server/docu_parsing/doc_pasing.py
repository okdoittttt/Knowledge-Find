from unstructured.partition.auto import partition

elements = partition(filename="../files/example.pdf")

print("\n\n".join([str(el) for el in elements]))