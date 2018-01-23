# alexa-soundcloud

stream and control your soundcloud music from alexa

This is not an offical app. According to this [blog post](https://techdev.io/de/developer-blog/the-complete-guide-to-running-an-alexa-soundcloud-skill) it looks like there is no support from soundcloud.

But with a little bit of configuration, you can easily build your own soundcloud alexa skill.

(The following guide aussumes that you have an amazon developer account and that you are a bit familiar with amazon web services)




## 1. Create the Alexa Skill

- login to [your alexa developer account](https://developer.amazon.com/edw/home.html#/)
- [create a new skill](https://developer.amazon.com/edw/home.html#/skill/create/)
- **Skill Information** provide a name and a invocation name (e.g. soundcloud) and click the radio button for audio player 
- **Interaction Model** (launch the new editor) open the `code` tab and paste `interactionModel_your_language.json` into the text field. click save and build the model
- **Configuration** (skip this for now, in the next step, we define the aws lambda function)


## 2. Deploy the code

- [create a new lambda function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/create)
- Name: alexa-soundcloud, Runtime: Python2.7, Execution Role: lambda_basic_execution
- hit the create function button
- add the trigger amazon skill kit
- upload the zip file
- enviroment variables


## Developer Comments

- check out [flask ask](https://github.com/johnwheeler/flask-ask). It makes developing skill very easy. Thanks :)
- also checkout the tutorials, ngrok + flask-ask is a great combination to speed up your development. 
- Creating new apps is currently disabled at soundcloud. I left my client_id in the code, so you can use that...
- I saw some examples where DynamoDB was used to save the playlist. This is not necessary, you can add it to your session attributes.
- For deploying my lambda function I prefer uploading the zip file. Instead of virtualenv I use the target option for pip install to install everything into the build directory.
