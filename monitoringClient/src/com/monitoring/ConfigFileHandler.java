package com.monitoring;

import java.io.*;
import java.util.ArrayList;
import java.util.UUID;

/**
 * Created by Patrick on 11/12/2016.
 */
public class ConfigFileHandler
{
    private String filePath = "./clientConfig";
    private File file;
    public final String CompID = "CompID";
    public final String URL = "URL";

    public ConfigFileHandler()
    {
        this.file = new File(filePath);
    }

    public String getMachineID()
    {
        String id;
        if(readConfigForSingleValue(CompID) != null)
            id = readConfigForSingleValue(CompID);
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
            FileWriter fileWriter = new FileWriter(file.getName(),true);
            BufferedWriter bufferWritter = new BufferedWriter(fileWriter);
            bufferWritter.write(String.format("%s:%s\n", label, element));
            bufferWritter.close();
        }
        catch(Exception e)
        {e.printStackTrace();}
    }

    private String readConfigForSingleValue(String label)
    {
        String rv = null;
        try
        {
            File file = new File(filePath);

            if(!file.exists())
                file.createNewFile();

            BufferedReader br = new BufferedReader(new FileReader(filePath));

            String line;
            while((line = br.readLine()) != null)
            {
                if(line.startsWith(label))              //will get last item
                    rv = line.split(":", 2)[1];        //not very safe.
            }
            br.close();
        }
        catch (FileNotFoundException e)
        {e.printStackTrace();}
        catch (IOException e)
        {e.printStackTrace();}

        return rv;
    }

    private ArrayList<String> readConfigForValueSet(String label)
    {
        ArrayList<String> rv = new ArrayList<String>();
        try
        {
            BufferedReader br = new BufferedReader(new FileReader(filePath));

            String line;
            while((line = br.readLine()) != null)
            {
                if(line.startsWith(label))
                    rv.add(line.split(":", 2)[1]);
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
        return readConfigForSingleValue(URL);
    }

    public void setURL(String url)
    {
        writeConfig(URL, url);
    }

    public ArrayList<String> getSensors()
    {
        return readConfigForValueSet("SENSOR");
    }

    public void addSensor(String sensorType)
    {
        writeConfig("SENSOR", sensorType);      //no checking yet
    }

    public boolean hasUrl()
    {
        return readConfigForSingleValue(URL) != null;
    }
}
