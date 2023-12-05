from setuptools import setup

setup(
    name='TalkGTTS',
    version='0.2',
    packages=['TalkGTTS'],
    url='https://github.com/Talklet123/Talk-Module',
    license='MIT',
    author='Talklet123',
    author_email='developer1234567890234@yahoo.com',
    description='Uses GTTS to make it talk.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'gTTS>=2.4.0',
	'playsound>=1.3.0'
    ],
)

