package me.lc4t.Crawler;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Dictionary;
import java.util.List;
import java.util.Map;

import org.jsoup.nodes.Document;



// 目录分析->输出数据结构
/**
 * 
 * data struct
 * 
 * server needs:
 * 		[vector]:rootURL,name,author,total,updateTime,status,dataFrom,introduction,...
 * 		{
 * 			id,
 * 			herf,
 * 			title,
 * 			content
 * 			
 * 		}->having total
 * 
 * 
 * user needs:
 * 		[vector]:name,author,total,updateDate,status,dataFrom,introduction,...
 * 		{
 * 			title,
 * 			content
 * 		}->having total
 *
 */
public class CatalogStruct
{
	protected Document rawHTML;
	private String rootURL;
	private String name;
	private String author;
	private int total;
	private String latest;
	private String updateTime;
	private String status;
	private String dataFrom;
	private String introduction;
	private List<Map> catalog = new ArrayList<Map>();
	
	
	public CatalogStruct()
	{
		// nothing
	}
	
	public CatalogStruct(Document catalog,String url) throws IOException
	{
		Functions temp = new Functions();
		this.rootURL = temp.strip(url, '/');
		this.rawHTML = catalog;
		
		SitesJudge judger = new SitesJudge();
		Site site = judger.judge(url);
		
		site.setRawURL(url);
		site.setCatalog(rawHTML);
		this.name = site.getName();
		this.author = site.getAuthor();
		this.total = site.getTotal();
		this.latest = site.getLatest();
		this.updateTime = site.getUpdateTime();
		this.status = site.getStatus();
		this.dataFrom = site.getDataFrom();
		this.introduction = site.getIntroduction();
		this.catalog = site.getCatalog();
		this.total = site.getTotal();
		this.catalog = site.getContent(this.catalog);
		

		
		
		
	}
	
	public String getRootURL()
	{
		return this.rootURL;
	}
	
	public String getName()
	{
		return this.name;
	}
	
	public String getAuthor()
	{
		return this.author;
	}
	
	public int getTotal()
	{
		return this.total;
	}
	
	public String getUpdateTime()
	{
		return this.updateTime;
	}
	
	public String getStatus()
	{
		return this.status;
	}
	
	public String getDataFrom()
	{
		return this.dataFrom;
	}
	
	public String getIntroduction()
	{
		return this.introduction;
	}
	
	public List getCatalog()
	{
		return this.catalog;
	}
	

	
	
	
	public void printCatalog2User()
	{
//		 * user needs:
//			 * 		[vector]:name,author,total,updateDate,status,dataFrom,introduction,...
//			 * 		{
//			 * 			content
//			 * 		}->having total
		System.out.println("URL: " + this.rootURL);
		System.out.println("author: " + this.author);
		System.out.println("total: " + this.total);
		System.out.println("latest: " + this.latest);
		System.out.println("updateTime: " + this.updateTime);
		System.out.println("status: " + this.status);
		System.out.println("dataFrom: " + this.dataFrom);
		System.out.println("introduction: " + this.introduction);
//		System.out.println("List: " + this.catalog);
		
//		System.out.println()

		
			 
	}
	
	
	public void export2File() throws IOException
	{
//		 * user needs:
//			 * 		[vector]:name,author,total,updateDate,status,dataFrom,introduction,...
//			 * 		{
//			 * 			content
//			 * 		}->having total
		
		
		File file = new File(this.name + ".txt");
		if (!file.exists())
		{
			file.createNewFile();
		}
		FileWriter fileWritter = new FileWriter(file.getName(),false);
        BufferedWriter bufferWritter = new BufferedWriter(fileWritter);
       
        
        bufferWritter.write("URL: " + this.rootURL + "\n");

        bufferWritter.write("author: " + this.author + "\n");
        bufferWritter.write("total: " + this.total + "\n");
        System.out.println("latest: " + this.latest + "\n");
        bufferWritter.write("updateTime: " + this.updateTime + "\n");
        bufferWritter.write("status: " + this.status + "\n");
        bufferWritter.write("dataFrom: " + this.dataFrom + "\n");
        bufferWritter.write("introduction: " + this.introduction + "\n");
        
        for(int i = 0; i < this.total; i++)
        {
        	bufferWritter.write("\n" + (String)this.catalog.get(i).get("title") +"\n");
        	bufferWritter.write((String)this.catalog.get(i).get("content"));
        	System.out.println("OK" + (i+1) + "/" + this.total);
        }
        
        
        
        bufferWritter.close();
		
		
		
//		System.out.println()

		
			 
	}

	
	
};


































