import subprocess

def configure_deepeval():
    try:
        subprocess.run([
            "deepeval", "set-local-model",
            "--model-name=llama3",
            "--base-url=http://ollama:11434/",
            "--api-key=ollama"
        ], check=True)
        print("DeepEval est maintenant configuré pour utiliser le modèle local d’Ollama.")
    except subprocess.CalledProcessError as e:
        print("Échec de la configuration de DeepEval :", e)

if __name__ == "__main__":
    configure_deepeval()
