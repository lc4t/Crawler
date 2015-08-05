
package me.lc4t.Crawler;

import java.sql.*;
import java.util.Scanner;

import org.sqlite.JDBC;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;




public class Crawler
{
	
	
	
	
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, SQLException
	{
		
		System.out.println(" ‰»Îƒø¬º“≥√ÊURL: ");
		Scanner scanner = new Scanner(System.in);

		BookAnalyze analyzer = new BookAnalyze(scanner.nextLine());
		CatalogStruct book = (CatalogStruct)(analyzer.getCatalog("text"));
//		book.printCatalog2User();
		book.export2File();
		
		
		
		
		
	}
}





