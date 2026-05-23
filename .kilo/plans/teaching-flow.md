The idea is to teach everything in a flow 

section 01 : Setup of K8 cluster and different namespaces thats all
section 02 : Deploying the airline app in different namspaces and how to use kubectl to interact with the cluster
section 03 : Showing the issue with all this deployment that is related to cost. Like missing tags etc. Also show an issue with a deployment being wrong (still running) but we don't know whom to ask about it.
section 04 : Building the python agent that runs locally connects to k8 cluster and generates a report about the cost of the cluster and also shows the issues with the deployment. But it lacks decision flow and creating issue in our tracker.
section 05 : setting up bedrock and adding bedrock to our agent python local and show how llm can help us to create a decision flow and bring more clarity to the report than before. Run it locally and explain this output and how clean it is.
section 06 : Deploying our issue tracker docker image and explain that its similar to jira and show an endpoint (fastapi doc) to show how to use /raise-issue and how the payload should look like
section 07 :  Add a section to our python code to now be able to gather required metadata from K8 and send it to bedrock with prompt, config , mapping of managers etc and then get the bedrock outut and create an issue in our issue tracker.
section 08 : We need this agent to also run on K8 so we now show the same code being dockerized and then deployed in a different namespace in K8 cluster after deployment set a cron job to run it 1 time and then show the output in the the issue tracker.


Note : Each section should have a full detailed guide . ofcourse as we move ahead we expect some previous resources to be present in this case just mention in the guide to refer to previous section for that resource.