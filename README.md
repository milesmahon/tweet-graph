Uses <a href="https://github.com/twitter/twurl">Twurl</a> to pull tweets from Bernie Sanders, counts instances of keywords
and uses matplotlib.pyplot to graph them. 
There are other ways of doing this but twurl via subprocess was the simplest now that the API requires OAuth.

Setting up twurl just requires you make an application on twitter (to get a consumer key and secret) and then
follow twurl's instructions for OAuth authentication.

Read about the <a href="https://dev.twitter.com/rest/reference/get/statuses/user_timeline">twitter API</a> (specifically what this project uses).

Output looks like:

<div align="center">
        <img width="45%" src="imgs/BSGraph.png" title="Graph"</img>
        <img height="0" width="8px">
        <img width="45%" src="imgs/BSPMFGraph.png" title="PMF"></img>
</div>

Yes, the graphs look identical. The difference is just that the PMF is a better way of conveying the information
(as ratios over total).

