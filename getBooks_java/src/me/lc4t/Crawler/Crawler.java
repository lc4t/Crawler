
package me.lc4t.Crawler;


import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;




public class Crawler
{
	
	
	
	
	
	public static void main(String[] args) throws IOException, ClassNotFoundException
	{
		
//		System.out.println("输入目录页面URL: ");
//		Scanner scanner = new Scanner(System.in);

//		BookAnalyze analyzer = new BookAnalyze(scanner.nextLine());
//		CatalogStruct book = (CatalogStruct)(analyzer.getCatalog("text"));
//		book.printCatalog2User();
//		book.export2File();
		
		String url = "http://www.heikexs.com";
		Document catalogHTML = Jsoup.connect(url).get();	//获取此url内容
		
		String text = catalogHTML.select("div.novel").toString();
		
		Pattern pattern = Pattern.compile("<p>最新章节：<a href=\".*\" title=\"(.*)\"");  
	    Matcher matcher = pattern.matcher(text);
	    while (matcher.find())
	    {
	    	System.out.println(matcher.group(1));
	    }
	    
		System.out.print(text);

		
		
		
	}
}





