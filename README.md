
# SmorgasBoard - Just the Juicy Bits


## What is this repo?
If you're reading this, you're probably considering working with me in some capacity. Good news: this repo is for you! It contains snippets from a SaaS project I designed and built. The AWS Lambdas that powered it are here, as is the SQL schema, the REST API CloudFormation files, and the whole frontend[^1]. I've adjusted the directory structure to make it a bit easier to find the interesting stuff at a glance — the code I wrote — even if you're not familiar with AWS.

## What was the project?
SmorgasBoard was a virtual photo booth pitched at weddings and events. Photos would be presented in real-time at a wedding or party on a large TV/projector screen running my webapp. Party attendees added photos instantly from their phones by scanning a QR code on the TV/projector. Thus, a blank screen would evolve into an animated photo collage over the course of an evening. All photos would later be sent to the event host to download.

## Can you talk about the tech stack?
Of course! SmorgasBoard was built for AWS using a serverless architecture. I used an Infrastructure-as-Code approach, made somewhat easier by AWS Amplify. The data layer was S3 for storing photos and an Amazon MySQL RDS instance for everything else. Auth was handled via AWS Cognito integrations. Requests were routed from AWS API Gateway to Lambda functions, written in Python, which handled all business logic. The frontend was Angular (using Typescript, naturally) and relied on Bootstrap components. Real-time updates were piped to clients using WebSockets, also sitting atop API Gateway. Payments were handled with a Stripe API integration. Blog posts were embedded on the site with a WordPress integration.

## Sounds cool! How can I try this out?
This project is now shuttered, but you can still see an [archived version](https://web.archive.org/web/20220210231859/http://smorgasboard.io/) on the Wayback Machine.

<br><br><br><br>

Unless otherwise marked, all code is Copyright © Sam Goldstein, 2021.

[^1]: Minus some environment stuff.