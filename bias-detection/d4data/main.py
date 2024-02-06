import csv
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("d4data/bias-detection-model")
model = TFAutoModelForSequenceClassification.from_pretrained(
    "d4data/bias-detection-model"
)

classifier = pipeline(
    "text-classification", model=model, tokenizer=tokenizer
)  # cuda = 0,1 based on gpu availability

# read input data
input = []
with open("input.csv", newline="") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=";", quotechar='"')

    # skip header
    next(csv_reader, None)

    for row in csv_reader:
        input.append(
            {
                "sentence": row[0],
                "expected_label": row[1],
                "expected_score": row[2],
            }
        )
print("✅ input.csv successfully loaded")

# classify input
result = []
for input in input:
    res = classifier(input["sentence"])[0]

    result.append(
        {
            "sentence": input["sentence"],
            "label": res["label"],
            "score": res["score"],
            "expected_label": input["expected_label"],
            "expected_score": input["expected_score"],
        }
    )
print("✅ input successfully classified loaded")

# export result
with open("results.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(
        csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # write header
    csv_writer.writerow(
        [
            "sentence",
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
