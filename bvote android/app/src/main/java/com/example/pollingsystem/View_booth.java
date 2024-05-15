package com.example.pollingsystem;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

public class View_booth extends AppCompatActivity implements JsonResponse{


    ListView l1;
    String[] booth_id,booth,val;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_booth);
        l1=(ListView)findViewById(R.id.lvbooths);

        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) View_booth.this;
        String q = "/View_booth?district_ids="+View_district.district_ids;
        q=q.replace(" ","%20");
        JR.execute(q);

    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method = jo.getString("method");
            if (method.equalsIgnoreCase("View_booth")) {
                String status = jo.getString("status");
                Log.d("pearl", status);
                Toast.makeText(getApplicationContext(), status, Toast.LENGTH_SHORT).show();
                if (status.equalsIgnoreCase("success")) {

                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");

                    booth_id = new String[ja1.length()];
                    booth = new String[ja1.length()];

                    val = new String[ja1.length()];


                    for (int i = 0; i < ja1.length(); i++) {


                        booth_id[i] = ja1.getJSONObject(i).getString("booth_id");
                        booth[i] = ja1.getJSONObject(i).getString("booth");;


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i] = "Booth : " + booth[i];


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
        Intent b = new Intent(getApplicationContext(), View_district.class);
        startActivity(b);
    }
}

