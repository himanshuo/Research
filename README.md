#Using Social Media as A Language Tutor Research

Social media provides rich resource for learning a (new) language. Taken English as an example, the word usage patterns on twitter and forums are dramatically different from that in text books or dictionary gloss. New words, phrases and slang are created everyday by ordinary users. The goal of this project is to build statistic language models to capture such unique language usage patterns and rewrite the *regular* input English sentences into more popular and domain-specific sentences so that the rewritten sentence can quickly attract more attention in the social network.





#Usage
<ol>
<li>Create a developer account on Twitter. </li>
<li>Create a Twitter application.</li>
<li>Create a file called constants.py in the same directory.</li>

<li>constants.py should look like(also in constants-sample.py):</li>
<br/><br/>
BASE_URL="https://stream.twitter.com/1.1/statuses/"<br/>
TOKEN_URL=BASE_URL+"filter.json"<br/>
SAMPLE_URL=BASE_URL+"sample.json"<br/>
<br/>
CONSUMER_KEY=<consumer key><br/>
CONSUMER_SECRET=<consumer secret><br/>
OAUTH_TOKEN=<oauth token><br/>
ACCESS_TOKEN_SECRET=<access token secret><br/>
<br/>
oauth_signature_method="HMAC-SHA1"
 
 
 <li>run python3 get_data.py</li>
</ol>



This research is done by Professor Hongning Wang with help from UVA students Himanshu Ojha, and ...
 