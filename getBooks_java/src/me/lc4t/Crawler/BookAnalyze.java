package me.lc4t.Crawler;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class BookAnalyze
	{
		private Document catalogHTML;	//Ŀ¼
		private CatalogStruct catalogText;
		public BookAnalyze()		
		{
			// nothing
		}
		
		public BookAnalyze(String url) throws IOException
		{
			this.catalogHTML = Jsoup.connect(url).get();	//��ȡ��url����
			catalogFormatter(this.catalogHTML, url);				//����Ŀ¼
		}
		
		protected void catalogFormatter(Document catalogHTML, String url) throws IOException	//��Ŀ¼����Ϊ�涨���ݽṹ
		{
			CatalogStruct catalogText = new CatalogStruct(catalogHTML, url);
			this.catalogText = catalogText;
		}
		
		
		public Object getCatalog(String format)				//�û���ȡĿ¼
		{
		    Pattern htmlPattern = Pattern.compile("(?i)html");  
		    Matcher htmlMatcher = htmlPattern.matcher(format);
		    
		    Pattern textPattern = Pattern.compile("(?i)text");  
		    Matcher textMatcher = textPattern.matcher(format);

		    if(htmlMatcher.find())				//html��ʽ
		    {  
		    	return this.catalogHTML;
	        }  
		    else if (textMatcher.find())		//�ڲ���ʽ,���Ķ�ģʽ,�ṹ��Ƕ��getter
		    {
		    	return (CatalogStruct)this.catalogText;
		    }
		    else
		    {
		    	return null;
		    }
			
		}
		
	};




