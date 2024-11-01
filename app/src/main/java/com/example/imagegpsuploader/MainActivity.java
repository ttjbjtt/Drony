package com.example.imagegpsuploader;

import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    // 로그 태그 정의
    private static final String TAG = "MainActivity";
    // GPSManager 객체 선언 (GPS 데이터 수집 담당)
    private GPSManager gpsManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gpsManager = new GPSManager(this);
        DataSender dataSender = new DataSender();

        // 위치 권한 요청 및 GPS 데이터 수집 후 서버로 전송
        gpsManager.requestLocationPermission();
        gpsManager.getCurrentLocation(gpsData -> {
            if (gpsData != null) {
                dataSender.sendData(
                        gpsData.getLatitude(),
                        gpsData.getLongitude(),
                        gpsData.getAltitude(),
                        gpsData.getHeading()
                );
            }
        });
    }

    // 권한 요청에 대한 응답 처리
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        // GPSManager의 권한 요청 코드와 일치하는지 확인
        if (requestCode == GPSManager.REQUEST_LOCATION_PERMISSION) {
            // 권한이 허용되었을 때만 위치 데이터를 수집
            gpsManager.getCurrentLocation(gpsData -> {
                if (gpsData != null) {
                    // GPS 데이터 수집 성공 Toast 메시지 출력
                    Toast.makeText(MainActivity.this, "GPS 데이터 수집 성공", Toast.LENGTH_SHORT).show();

                    // 수집된 GPS 데이터 로그 출력
                    Log.d(TAG, "수집된 GPS 데이터: " + gpsData.toString());

                    // 추가 확인 로그
                    Log.d(TAG, "GPS 데이터가 정상적으로 수집되었습니다. 다음 단계로 진행");
                } else {
                    // GPS 데이터가 null인 경우의 로그 출력
                    Log.e(TAG, "GPS 데이터가 null입니다.");
                }
            });

        }
    }
}
