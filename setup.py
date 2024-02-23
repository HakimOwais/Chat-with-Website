from setuptools import find_packages,setup

setup(
    name='chatwithwebsite',
    version='0.0.1',
    author='Owais Bin Mushtaq',
    author_email='owaisibnmushtaq@gmail.com',
    install_requires=["openai","langchain==0.1.1","streamlit==1.28.0","python-dotenv",
                      "langchain-openai==0.0.2.post1","beautifulsoup4==4.12.2"],
    packages=find_packages()
)




