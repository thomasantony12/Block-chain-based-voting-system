package com.example.pollingsystem;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.util.Log;

public class JsonReq extends AsyncTask<String, Void, String> {
	
	public JsonResponse json_response = null;
//	SharedPreferences sh;
//	Context context;
	@Override
	protected String doInBackground(String... arg) {
		// TODO Auto-generated method stub
		HttpURLConnection c = null;
//		sh = PreferenceManager.getDefaultSharedPreferences(context);
//		String ip=sh.getString("ipval", "");
		String jsonReqUrl = "http://" + IPsettings.ip + "/api"+arg[0];
		Log.d("pearl",jsonReqUrl);
		 try {
	            URL u=new URL(jsonReqUrl);
	            c=(HttpURLConnection) u.openConnection();
	            c.setRequestMethod("GET");
	            c.setRequestProperty("Content-length","0");
	            c.setUseCaches(false);
	            c.setAllowUserInteraction(false);
	            c.connect();
	            int status=c.getResponseCode();
	            Log.d("julyy",jsonReqUrl);
	            switch (status)
	            {
	                case 200:
	                case 201:
	                    BufferedReader br=new BufferedReader(new InputStreamReader(c.getInputStream()));
	                    StringBuilder sb=new StringBuilder();
	                    String line = "";
	                    while ((line=br.readLine())!=null)
	                    {
	                        sb.append(line+"\n");
	                    }
	                    br.close();
	                    return sb.toString();
	                default:
	                    return "";
	            }
	        } catch (ProtocolException e) {
	            e.printStackTrace();
	        } catch (MalformedURLException e) {
	            e.printStackTrace();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
		return "";
	}

	@Override
	protected void onPostExecute(String result) {
		// TODO Auto-generated method stub
		super.onPostExecute(result);
		Log.d("july1",result);
		try {
			JSONObject jo = new JSONObject(result);
			json_response.response(jo);
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}	
}