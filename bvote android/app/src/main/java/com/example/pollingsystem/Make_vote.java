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

public class Make_vote extends AppCompatActivity implements JsonResponse, AdapterView.OnItemClickListener{


    ListView l1;
    String[] candidate_id,cname,election_date,declared_on,estatus,val;
    public  static String candidate_ids,estatuss;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_make_vote);
        l1=(ListView)findViewById(R.id.lvvotw);
        l1.setOnItemClickListener(this);

        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) Make_vote.this;
        String q = "/Make_vote_candidate?login_id="+Login.logid+"&election_ids="+View_election_status.election_ids;
        q=q.replace(" ","%20");
        JR.execute(q);

    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method = jo.getString("method");
            if (method.equalsIgnoreCase("Make_vote_candidate")) {
                String status = jo.getString("status");
                Log.d("pearl", status);
                Toast.makeText(getApplicationContext(), status, Toast.LENGTH_SHORT).show();
                if (status.equalsIgnoreCase("success")) {

                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");

                    candidate_id = new String[ja1.length()];
                    cname = new String[ja1.length()];


                    val = new String[ja1.length()];


                    for (int i = 0; i < ja1.length(); i++) {


                        candidate_id[i] = ja1.getJSONObject(i).getString("candidate_id");
                        cname[i] = ja1.getJSONObject(i).getString("cname");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i] = "Candidate Name: " + cname[i];


                    }
                    ArrayAdapter<String> ar = new ArrayAdapter<String>(getApplicationContext(), R.layout.cust_list, val);
                    l1.setAdapter(ar);


                } else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }

            if(method.equalsIgnoreCase("make_vote"))
            {
                String status=jo.getString("status");
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
                if(status.equalsIgnoreCase("success"))
                {
                    Toast.makeText(getApplicationContext()," Successfully Added!", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(), View_election_status.class));
                }
                else if(status.equalsIgnoreCase("Already Voted"))
                {
                    Toast.makeText(getApplicationContext()," Already Voted", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(), View_election_status.class));
                }
                else{
                    Toast.makeText(getApplicationContext(),"Failed", Toast.LENGTH_LONG).show();
                }
            }


        } catch (Exception e) {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
        }


    }


    public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
        // TODO Auto-generated method stub
        candidate_ids = candidate_id[arg2];


            final CharSequence[] items = {"MAKE VOTE", "Cancel"};

            AlertDialog.Builder builder = new AlertDialog.Builder(Make_vote.this);

            // builder.setTitle("Add Photo!");
            builder.setItems(items, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int item) {
                    if (items[item].equals("MAKE VOTE")) {

                        JsonReq JR=new JsonReq();
                        JR.json_response=(JsonResponse) Make_vote.this;
                        String q = "/make_vote?login_id="+Login.logid+"&candidate_ids="+candidate_ids+"&election_ids="+View_election_status.election_ids;
                        q=q.replace(" ","%20");
                        JR.execute(q);

                    } else if (items[item].equals("Cancel")) {
                        dialog.dismiss();
                    }
                }

            });
            builder.show();
        }
//        else if (estatuss.equalsIgnoreCase("completed")) {
//
//            final CharSequence[] items = {"VIEW RESULT", "Cancel"};
//
//            AlertDialog.Builder builder = new AlertDialog.Builder(View_election_status.this);
//
//            // builder.setTitle("Add Photo!");
//            builder.setItems(items, new DialogInterface.OnClickListener() {
//                @Override
//                public void onClick(DialogInterface dialog, int item) {
//                    if (items[item].equals("VIEW RESULT")) {
//
//                        startActivity(new Intent(getApplicationContext(), View_result.class));
//                    } else if (items[item].equals("Cancel")) {
//                        dialog.dismiss();
//                    }
//                }
//
//            });
//            builder.show();
//        }



    public void onBackPressed() {
        // TODO Auto-generated method stub
        super.onBackPressed();
        Intent b = new Intent(getApplicationContext(), View_election_status.class);
        startActivity(b);
    }
}

