package me.lc4t.Crawler;

public class Functions
{
	public Functions()
	{
		// should be nothing
	}
	
	public String lstrip(String str,char c)	//delete char c from left of str
	{
		if (str.charAt(0) == c)
		{
			return str.substring(1);
		}
		else
		{
			return str;
		}
	}
	
	public String rstrip(String str,char c)	//delete char c from right of str
	{
		int length = str.length();
		if (str.charAt(length - 1) == c)
		{
			return str.substring(0,length - 1);
		}
		else
		{
			return str;
		}
	}
	
	
	public String strip(String str,char c)	//delete char c from right of str
	{
		str = lstrip(str,c);
		str = rstrip(str,c);
		return str;
	}
};
