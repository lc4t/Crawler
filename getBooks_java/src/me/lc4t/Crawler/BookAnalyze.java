package me.lc4t.Crawler;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class BookAnalyze
	{
		private Document catalogHTML;	//目录
		private CatalogStruct catalogText;
		public BookAnalyze()		
		{
			// nothing
		}
		
		public BookAnalyze(String url) throws IOException
		{
			this.catalogHTML = Jsoup.connect(url).get();	//获取此url内容
			catalogFormatter(this.catalogHTML, url);				//分析目录
		}
		
		protected void catalogFormatter(Document catalogHTML, String url) throws IOException	//将目录分析为规定数据结构
		{
			CatalogStruct catalogText = new CatalogStruct(catalogHTML, url);
			this.catalogText = catalogText;
		}
		
		
		public Object getCatalog(String format)				//用户读取目录
		{
		    Pattern htmlPattern = Pattern.compile("(?i)html");  
		    Matcher htmlMatcher = htmlPattern.matcher(format);
		    
		    Pattern textPattern = Pattern.compile("(?i)text");  
		    Matcher textMatcher = textPattern.matcher(format);

		    if(htmlMatcher.find())				//html格式
		    {  
		    	return this.catalogHTML;
	        }  
		    else if (textMatcher.find())		//内部格式,可阅读模式,结构内嵌入getter
		    {
		    	return (CatalogStruct)this.catalogText;
		    }
		    else
		    {
		    	return null;
		    }
			
		}
		
	};




