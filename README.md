# BigDataManagement-PageRank
A PageRank score for tennis players, using Xpath, Crawling &amp; Ranking
# Q1
Consider the Wikipedia pages of professional tennis players, e.g., https://en.wikipedia.org/wiki/Andy_Ram.   
We Looked at the HTML sources of the pages and try to write XPath expressions with:  
**Input:** HTML contents of a Wikipedia page (in the English version, en.wikipedia.org) of any tennis player, e.g., https://en.wikipedia.org/wiki/Andy_Ram.  
**Output:** URLs of Wikipedia pages of related tennis players.  
We define a related tennis player as one who played a match with the current player or was the coach of the current player.  
 
     
# Q2  
We Wrote a function def crawl(url,xpaths) whose purpose is to crawl pages of tennis players in Wikipedia.  
**Input:** *[a]* url - a string containing the URL of the start page (e.g., https://en.wikipedia.org/wiki/Andy_Ram).  
*[b]* xpaths - a list of strings representing legal XPath expressions.  
**Output:** a list of lists. Each inner list contain two strings:  
The first is the source URL, and the second is the URL of a page detected in the source URL by the crawler. 
The function will use the xpaths to extract a set of URLs from the web page.
These URLs also crawled in order of priority:  
We Keep counts for the number of times each URL was found. URLs seen the highest number of times have the highest priority.  
In total, at most 100 URLs were crawled in this manner, and only URLs of en.wikipedia.org.

# Q3
A PageRank score for tennis players.  
**Input:** list of lists in the format of the output of crawl from Q2.  
The function treats each inner list [X, Y] as a link from X to Y.  
We used the **random surfer model**:  
i. The graph nodes are all the URLs in the input . 
ii. Start from a random node . 
iii. At each step, the surfer decides with probability 0.85 to follow a link,  
or with probability 0.15 to jump to a random tennis player.  
If there are no outgoing links, always jump to a random member.  
Repeat this process 200,000 step. Record the number of times you have visited each page in the first 100,000 steps, and in the last 100,000 steps.  
The PageRank of each member is the number of times it was visited divided by the number of steps.  
**Output:** a dict where the keys are URLs and the values are the scores computed from the first and last 100,000 steps.  
