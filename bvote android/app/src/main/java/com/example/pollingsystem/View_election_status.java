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

public class View_election_status extends AppCompatActivity implements JsonResponse, AdapterView.OnItemClickListener{

    ListView l1;
    String[] election_id,body,election_date,declared_on,estatus,val;
    public  static String election_ids,estatuss;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_election_status);
        l1=(ListView)findViewById(R.id.lvelection);
        l1.setOnItemClickListener(this);

        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) View_election_status.this;
        String q = "/View_election_status";
        q=q.replace(" ","%20");
        JR.execute(q);

    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method = jo.getString("method");
            if (method.equalsIgnoreCase("View_election_status")) {
                String status = jo.getString("status");
                Log.d("pearl", status);
                Toast.makeText(getApplicationContext(), status, Toast.LENGTH_SHORT).show();
                if (status.equalsIgnoreCase("success")) {

                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");

                    election_id = new String[ja1.length()];
                    body = new String[ja1.length()];
                    election_date = new String[ja1.length()];
                    declared_on = new String[ja1.length()];
                    estatus = new String[ja1.length()];

                    val = new String[ja1.length()];


                    for (int i = 0; i < ja1.length(); i++) {


                        election_id[i] = ja1.getJSONObject(i).getString("election_id");
                        body[i] = ja1.getJSONObject(i).getString("body");
                        election_date[i] = ja1.getJSONObject(i).getString("election_date");
                        declared_on[i] = ja1.getJSONObject(i).getString("declared_on");
                        estatus[i] = ja1.getJSONObject(i).getString("status");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i] = "Election Name: " + body[i]+"\nElection Date : "+election_date[i]
                                +"\nDeclared On : "+declared_on[i]+"\nStatus : "+estatus[i];


                    }
                    ArrayAdapter<String> ar = new ArrayAdapter<String>(getApplicationContext(), R.layout.cust_list, val);
                    l1.setAdapter(ar);


                } else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }

//            if(method.equalsIgnoreCase("make_vote"))
//            {
//                String status=jo.getString("status");
//                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
//                if(status.equalsIgnoreCase("success"))
//                {
//                    Toast.makeText(getApplicationContext()," Successfully Added!", Toast.LENGTH_LONG).show();
//                    startActivity(new Intent(getApplicationContext(), View_election_status.class));
//                }
//                else{
//                    Toast.makeText(getApplicationContext(),"Failed", Toast.LENGTH_LONG).show();
//                }
//            }


        } catch (Exception e) {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
        }


    }


    public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
        // TODO Auto-generated method stub
        election_ids = election_id[arg2];
        estatuss = estatus[arg2];

        if (estatuss.equalsIgnoreCase("started")) {

            final CharSequence[] items = {"MAKE VOTE", "Cancel"};

            AlertDialog.Builder builder = new AlertDialog.Builder(View_election_status.this);

            // builder.setTitle("Add Photo!");
            builder.setItems(items, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int item) {
                    if (items[item].equals("MAKE VOTE")) {

                        startActivity(new Intent(getApplicationContext(), Make_vote.class));

                    } else if (items[item].equals("Cancel")) {
                        dialog.dismiss();
                    }
                }

            });
            builder.show();
        } else if (estatuss.equalsIgnoreCase("completed")) {

            final CharSequence[] items = {"VIEW RESULT", "Cancel"};

            AlertDialog.Builder builder = new AlertDialog.Builder(View_election_status.this);

            // builder.setTitle("Add Photo!");
            builder.setItems(items, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int item) {
                    if (items[item].equals("VIEW RESULT")) {

                        startActivity(new Intent(getApplicationContext(), View_result.class));
                    } else if (items[item].equals("Cancel")) {
                        dialog.dismiss();
                    }
                }

            });
            builder.show();
        }

    }

    public void onBackPressed() {
        // TODO Auto-generated method stub
        super.onBackPressed();
        Intent b = new Intent(getApplicationContext(), Home.class);
        startActivity(b);
    }
}

