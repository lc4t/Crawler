package me.lc4t.Crawler;

import java.io.IOException;
import java.util.Dictionary;
import java.util.List;
import java.util.Map;

import org.jsoup.nodes.Document;

public abstract class Site
{
	public Site()
	{
		
	}
	
	public void setRawURL(String rawURL)
	{
		
	}
	
	public void setCatalog(Document catalog)
	{
		
	}
	
	

	
	public String getName()
	{
		return null;
	}
	
	public String getAuthor()
	{
		return null;
	}
	
	private void setTotal(int total)
	{
		
	}
	
	public int getTotal()
	{
		return 0;
	}
	
	public String getLatest()
	{
		return null;
	}
	
	public String getUpdateTime()
	{
		return null;
	}
	
	public String getStatus()
	{
		return null;
	}
	
	public String getDataFrom()
	{
		return null;
	}
	
	public String getIntroduction()
	{
		return null;
	}
	
	public List getCatalog() throws IOException
	{
		return null;
	}
	
	public List getContent(List<Map> catalogList) throws IOException
	{
		return null;
	}
	
	
	
};