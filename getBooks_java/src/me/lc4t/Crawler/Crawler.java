
package me.lc4t.Crawler;


import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;




public class Crawler
{
	
	
	
	
	
	public static void main(String[] args) throws IOException, ClassNotFoundException
	{
		
		System.out.println(" ‰»Îƒø¬º“≥√ÊURL: ");
		Scanner scanner = new Scanner(System.in);

		BookAnalyze analyzer = new BookAnalyze(scanner.nextLine());
		CatalogStruct book = (CatalogStruct)(analyzer.getCatalog("text"));
//		book.printCatalog2User();
		book.export2File();
		

		
		
	}
}










