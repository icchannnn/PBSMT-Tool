from comet import download_model, load_from_checkpoint

if __name__ == '__main__':
    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)

    data = [
        {
            "src": "magandang gabi",
            "src_lang": "fil",
            "mt": "can i try your shoes?",
            "ref": "good evening"
        },
        {
            "src": "Kamusta ka?",
            "src_lang": "fil",
            "mt": "How are you?",
            "ref": "How are you?"
        },
        # Add more translation entries here
    ]

    # Evaluate a batch of translations
    model_output = model.predict(data, batch_size=1, gpus=1)

    for entry, result in zip(data, model_output):
        src_text = entry["src"]
        mt_text = entry["mt"]
        # print(f"Source: {src_text}")
        # print(f"MT: {mt_text}")
        print(model_output)
        print(result)  # Print the structure of the result
        print()
