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
		String status = this.catalog.select("meta[property=\"og:novel:status\"]").toString();	
	    Pattern pattern = Pattern.compile("content=\"(.*?)\"");  
	    Matcher matcher = pattern.matcher(status);
	    if (matcher.find())
	    {
	    	return matcher.group(1);
	    }
	    else
	    {
	    	return null;
	    }
	}
	
	public String getDataFrom()
	{
		return "笔趣阁";
	}

	public String getIntroduction()
	{
		String introduction = this.catalog.select("div[id=\"intro\"]").toString();
	    Pattern pattern = Pattern.compile("<p>(.*)</p>");  
	    Matcher matcher = pattern.matcher(introduction);
	    String str = "";
	    while(matcher.find())
	    {
	    	str += matcher.group(1);
	    }
	    return str;
	    
	    
	}
//	
	public List getCatalog() throws IOException
	{
		
		
		List<Map> catalogList = new ArrayList<Map>();
		
		String catalog = this.catalog.select("div[id=\"list\"]").toString();	
	    //(<a href=\"([0-9]{1,100}.html)\">(.*)</a>)|(<dt>\n{1,8}(.*))

	    Pattern pattern = Pattern.compile("<a href=\"([0-9]{1,100}.html)\">(.*)</a>");  
	    Matcher matcher = pattern.matcher(catalog);
	    
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
			String url = this.rawURL + "/" + catalogList.get(i).get("herf");

			Document tempHTML = Jsoup.connect(url).timeout(10000).get();
			String text = tempHTML.select("div[id=\"content\"]").toString();
			text = text.substring(45,text.length() - 7).replaceAll("&nbsp[;]{1,3}", " ").replaceAll("\\s<br>\\s\\s<br>", "");
			
			catalogList.get(i).put("content", text + "\n");
			System.out.println("getting: " + catalogList.get(i).get("title") + "	" + catalogList.get(i).get("id") + "/" + this.total);
			

		}
//		
    	
    	
    	
    	
    	

//		map.put("content", text);
//    	catalogList.add(map);
//		
    	
    	return catalogList;
//    	System.out.println(map.get("content"));
	}
}