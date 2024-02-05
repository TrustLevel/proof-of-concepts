import csv

from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained(
    "elozano/bert-base-cased-clickbait-news", from_pt=True
)
model = TFAutoModelForSequenceClassification.from_pretrained(
    "elozano/bert-base-cased-clickbait-news", from_pt=True
)

classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

input = []
with open("input.csv", newline="") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=";", quotechar='"')

    # skip header
    next(csv_reader, None)

    for row in csv_reader:
        input.append(
            {
                "id": row[0],
                "title": row[1],
                "author": row[5],
                "type": row[9],
                "expected_label": row[11],
                "expected_score": row[12],
            }
        )
print("✅ input.csv successfully loaded")

result = []
for input in input:
    res = classifier(input["title"])[0]

    result.append(
        {
            "id": input["id"],
            "title": input["title"],
            "author": input["author"],
            "type": input["type"],
            "label": res["label"],
            "score": res["score"],
            "expected_label": input["expected_label"],
            "expected_score": input["expected_score"],
        }
    )
print("✅ input successfully classified loaded")

with open("results.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(
        csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # write header
    csv_writer.writerow(
        [
            "id",
            "title",
            "author",
            "type",
            "label",
            "score",
            "expected_label",
            "expected_score",
        ]
    )

    # write content
    for entry in result:
        csv_writer.writerow(entry.values())

print("🎉 results successfully written to disk")
