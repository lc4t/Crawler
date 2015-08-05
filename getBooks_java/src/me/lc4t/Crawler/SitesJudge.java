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
	    
	    if(biqugeMatcher.find())
	    {
	    	BiqugeLa a = new BiqugeLa();
	    	return a ;
	    }
	    
	    
	    else
	    {
	    	return null;
	    }
	    
	    
	    
	    
	    
	    
	}
}