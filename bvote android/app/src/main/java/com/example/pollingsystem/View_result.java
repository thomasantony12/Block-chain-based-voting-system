package com.example.pollingsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

public class View_result extends AppCompatActivity implements JsonResponse{

    ListView l1;
    String[] cname,total_vote,val;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_result);

        l1=(ListView)findViewById(R.id.lvresult);

        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) View_result.this;
        String q = "/View_result?";
        q=q.replace(" ","%20");
        JR.execute(q);

    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method = jo.getString("method");
            if (method.equalsIgnoreCase("View_result")) {
                String status = jo.getString("status");
                Log.d("pearl", status);
                Toast.makeText(getApplicationContext(), status, Toast.LENGTH_SHORT).show();
                if (status.equalsIgnoreCase("success")) {

                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");


                    cname = new String[ja1.length()];
                    total_vote = new String[ja1.length()];


                    val = new String[ja1.length()];


                    for (int i = 0; i < ja1.length(); i++) {



                        cname[i] = ja1.getJSONObject(i).getString("cname");
                        total_vote[i] = ja1.getJSONObject(i).getString("total_vote");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i] = "Candidate Name:  " + cname[i] + "\nTotal Vote:  " + total_vote[i];


                    }
                    ArrayAdapter<String> ar = new ArrayAdapter<String>(getApplicationContext(), R.layout.cust_list, val);
                    l1.setAdapter(ar);


                } else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }


        } catch (Exception e) {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
        }


    }

    public void onBackPressed() {
        // TODO Auto-generated method stub
        super.onBackPressed();
        Intent b = new Intent(getApplicationContext(), View_election_status.class);
        startActivity(b);
    }
}

