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

public class View_candidate extends AppCompatActivity implements JsonResponse{

    ListView l1;
    String[] ename,cname,age,dob,place,city,state,phone,email,cstatus,val;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_candidate);

        l1=(ListView)findViewById(R.id.lvcandidate);

        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) View_candidate.this;
        String q = "/View_candidate?login_id="+Login.logid;
        q=q.replace(" ","%20");
        JR.execute(q);

    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method = jo.getString("method");
            if (method.equalsIgnoreCase("View_candidate")) {
                String status = jo.getString("status");
                Log.d("pearl", status);
                Toast.makeText(getApplicationContext(), status, Toast.LENGTH_SHORT).show();
                if (status.equalsIgnoreCase("success")) {

                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");

                    ename = new String[ja1.length()];
                    cname = new String[ja1.length()];
                    age = new String[ja1.length()];
                    dob = new String[ja1.length()];
                    place = new String[ja1.length()];
                    city=new String[ja1.length()];
                    state=new String[ja1.length()];
                    phone=new String[ja1.length()];
                    email=new String[ja1.length()];
                    cstatus=new String[ja1.length()];


                    val = new String[ja1.length()];


                    for (int i = 0; i < ja1.length(); i++) {


                        ename[i] = ja1.getJSONObject(i).getString("body");
                        cname[i] = ja1.getJSONObject(i).getString("cname");
                        age[i] = ja1.getJSONObject(i).getString("age");
                        dob[i] = ja1.getJSONObject(i).getString("dob");
                        place[i] = ja1.getJSONObject(i).getString("place");
                        city[i]=ja1.getJSONObject(i).getString("city");
                        state[i]=ja1.getJSONObject(i).getString("state");
                        phone[i]=ja1.getJSONObject(i).getString("phone");
                        email[i]=ja1.getJSONObject(i).getString("email");
                        cstatus[i]=ja1.getJSONObject(i).getString("candidate_status");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i] = "Election Name: " + ename[i] + "\nCandidate Name:  " + cname[i] + "\nAge:  " + age[i] + "\nDOB:  " + dob[i]
                                + "\nPlace:  " + place[i]+ "\nCity:  " + city[i]+ "\nState:  " + state[i]+ "\nPhone:  " + phone[i]
                                + "\nEmail:  " + email[i]+ "\nStatus:  " + cstatus[i];


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
        Intent b = new Intent(getApplicationContext(), Home.class);
        startActivity(b);
    }
    }

