package me.lc4t.Crawler;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SitesJudge
{
	public SitesJudge()
	{
		// none
	}
	
	public Site judge(String url)
	{
		Pattern biqugePattern = Pattern.compile("(?i)biquge.la");  
	    Matcher biqugeMatcher = biqugePattern.matcher(url);
	    Pattern heikexsPattern = Pattern.compile("(?i)heikexs.com");  
	    Matcher heikexsMatcher = heikexsPattern.matcher(url);

	    if(biqugeMatcher.find())
	    {
	    	BiqugeLa biquge = new BiqugeLa();
	    	return biquge ;
	    }
	    else if (heikexsMatcher.find())
	    {
	    	Heikexs heikexs = new Heikexs();
	    	return heikexs;
	    }
	    
	    else
	    {
	    	return null;
	    }
	    
	    
	    
	    
	    
	    
	}
}