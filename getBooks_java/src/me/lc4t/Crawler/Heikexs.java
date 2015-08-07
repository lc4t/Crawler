package me.lc4t.Crawler;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class Heikexs extends Site
{
	String rawURL;
	Document catalog ;
	int total;
	public Heikexs()
	{
		
	}
	
	public void setRawURL(String rawURL)
	{
		this.rawURL = rawURL;
	}
	
	public void setCatalog(Document catalog)
	{
		this.catalog = catalog;
	}
	

	public String getName()
	{
		
		String name = this.catalog.select("div.novel").toString();	//<meta property="og:title" content="XXXXXXX">
		Pattern pattern = Pattern.compile("<h1>(.*)</h1>");  
	    Matcher matcher = pattern.matcher(name);
	    if (matcher.find())
	    {
	    	return matcher.group(1);
	    }
	    else
	    {
	    	return null;
	    }
	}
	
	public String getAuthor()
	{
		String author = this.catalog.select("div.novel").toString();	
	    Pattern pattern = Pattern.compile("<p>作者：(.*)</p>");  
	    Matcher matcher = pattern.matcher(author);
	    if (matcher.find())
	    {
	    	return matcher.group(1);
	    }
	    else
	    {
	    	return null;
	    }
	}

	private void setTotal(int total)
	{
		this.total = total;
	}
	
	public int getTotal()
	{
		return this.total;
	}

	public String getLatest()
	{
		String updateTime = this.catalog.select("div.novel").toString();	
	    Pattern pattern = Pattern.compile("<p>最新章节：<a href=\".*\" title=\"(.*)\"");  
	    Matcher matcher = pattern.matcher(updateTime);
	    if (matcher.find())
	    {
	    	return matcher.group(1);
	    }
	    else
	    {
	    	return null;
	    }
	}

	public String getUpdateTime()
	{
		String updateTime = this.catalog.select("div.novel").toString();	
	    Pattern pattern = Pattern.compile("<p>更新时间：(.*)</p>");  
	    Matcher matcher = pattern.matcher(updateTime);
	    if (matcher.find())
	    {
	    	return matcher.group(1);
	    }
	    else
	    {
	    	return null;
	    }
	}
	
	public String getStatus()
	{
		return "Unknow";
	}
	
	public String getDataFrom()
	{
		return "黑客小说";
	}

	public String getIntroduction()
	{
		String introduction = this.catalog.select("div.jianjie").toString();
	    Pattern pattern = Pattern.compile("小说简介：\n(.*)\n</div>");  
	    Matcher matcher = pattern.matcher(introduction);
	    String str = "";
	    while(matcher.find())
	    {
	    	str += matcher.group(1).replace("<p>", "").replace("</p>","").replace("<br>", "\n");
	    }
	    return str;
	    
	    
	}
//	
	public List getCatalog() throws IOException
	{
		
		
		List<Map> catalogList = new ArrayList<Map>();
		
		String catalog = this.catalog.select("dl.cat_box").toString();	

		Pattern pattern = Pattern.compile("<dl class=\"cat_box\">[\\s]{1,10}([\\s\\S]*?)[\\s]{1,10}</dl>");  
	    Matcher matcher = pattern.matcher(catalog);
	    if (matcher.find())
	    {
	    	catalog = matcher.group(1);
	    }
	    pattern = Pattern.compile("<a href=\"([/\\d\\w]{1,100}.html)\" title=\"(.*)\">.*</a>");  
	    matcher = pattern.matcher(catalog);
	    
	    int i = 1;
        while (matcher.find()) 
        {
        	Map map = new HashMap();
        	map.put("id",i++);
        	map.put("herf", matcher.group(1));
        	map.put("title", matcher.group(2));
        	catalogList.add(map);
        } 

        setTotal(i - 1);

        return catalogList;

	}
	
	
	public List getContent(List<Map> catalogList) throws IOException
	{

		for (int i = 0; i < this.total; i++)
		{
			String url = this.rawURL +  catalogList.get(i).get("herf");

			Document tempHTML = Jsoup.connect(url).timeout(10000).get();
			String paragraph = tempHTML.select("p").toString();

			Pattern pattern = Pattern.compile("<p>(.*)</p>");  
		    Matcher matcher = pattern.matcher(paragraph);
		    
		    String text = "";
		    while (matcher.find())
		    {
		    	text += matcher.group(1);
		    }
		    
		    
			
			catalogList.get(i).put("content", text + "\n");
			System.out.println("getting: " + catalogList.get(i).get("title") + "	" + catalogList.get(i).get("id") + "/" + this.total);
			

		}

    	return catalogList;

	}
}