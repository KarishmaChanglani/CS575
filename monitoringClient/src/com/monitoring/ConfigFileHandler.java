package com.monitoring;

import java.io.*;
import java.util.UUID;

/**
 * Created by Patrick on 11/12/2016.
 */
public class ConfigFileHandler
{
    private String filePath = "./clientConfig";
    public final String CompID = "CompID";
    public final String URL = "URL";

    public String getMachineID()
    {
        String id;
        if(readConfig(CompID) != null)
            id = readConfig(CompID);
        else
        {
            id = UUID.randomUUID().toString();
            writeConfig(CompID, id);
        }
        return id;
    }

    private void writeConfig(String label, String element)
    {
        try
        {
            File file = new File(filePath);

            if(!file.exists())
                file.createNewFile();

            FileWriter fileWriter = new FileWriter(file.getName(),true);
            BufferedWriter bufferWritter = new BufferedWriter(fileWriter);
            bufferWritter.write(String.format("%s:%s", label, element));
            bufferWritter.close();
        }
        catch(Exception e)
        {e.printStackTrace();}
    }

    private String readConfig(String label)
    {
        String rv = null;
        try
        {
            BufferedReader br = new BufferedReader(new FileReader(filePath));

            String line;
            while((line = br.readLine()) != null)
            {
                if(line.startsWith(label))
                    rv = line;
            }
            br.close();
        }
        catch (FileNotFoundException e)
        {e.printStackTrace();}
        catch (IOException e)
        {e.printStackTrace();}

        return rv;
    }

    public String getURL()
    {
        return readConfig(URL);
    }

    public void setURL(String url)
    {
        writeConfig(URL, url);
    }
}
