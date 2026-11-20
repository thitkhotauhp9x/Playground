from app.libs.selenium_openai.main import ask


def main():
    response = ask(prompt="Giải giúp mình phương trình bậc hai x^2 + 2x - 6 = 0")
    print(response)
