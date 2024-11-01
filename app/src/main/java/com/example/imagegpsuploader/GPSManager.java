package com.example.imagegpsuploader;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.location.Location;
import android.util.Log;
import android.widget.Toast;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.tasks.OnSuccessListener;

public class GPSManager {
    // 로그 출력을 위한 태그
    private static final String TAG = "GPSManager";
    // 위치 권한 요청 코드
    public static final int REQUEST_LOCATION_PERMISSION = 1;

    // FusedLocationProviderClient는 위치 데이터를 제공하는 Google API 클라이언트
    private FusedLocationProviderClient fusedLocationProviderClient;
    // Activity 인스턴스를 통해 context를 제공하고 권한 요청을 처리
    private Activity activity;

    // GPSManager 생성자
    public GPSManager(Activity activity) {
        // Activity 인스턴스를 저장
        this.activity = activity;
        // FusedLocationProviderClient 초기화
        this.fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(activity);
    }

    // 위치 권한을 요청하는 메서드
    public void requestLocationPermission() {
        // 위치 권한이 부여되지 않은 경우 권한을 요청
        if (ContextCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            // 위치 권한을 사용자에게 요청
            ActivityCompat.requestPermissions(activity,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    REQUEST_LOCATION_PERMISSION);
        }
    }

    // 현재 위치를 가져오는 메서드
    public void getCurrentLocation(final OnSuccessListener<GPSData> listener) {
        // 위치 권한이 허용된 경우에만 위치 데이터 수집
        if (ContextCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            // 마지막으로 알려진 위치 데이터를 가져옴
            fusedLocationProviderClient.getLastLocation()
                    .addOnSuccessListener(activity, location -> {
                        // 위치 데이터가 존재하는 경우
                        if (location != null) {
                            // 위치 데이터를 GPSData 객체로 생성
                            GPSData gpsData = new GPSData(
                                    location.getLatitude(),     // 위도
                                    location.getLongitude(),    // 경도
                                    location.getAltitude(),     // 고도
                                    location.getBearing()       // 방향
                            );
                            // 성공 시, 수집된 GPSData 객체를 리스너를 통해 전달
                            listener.onSuccess(gpsData);
                            // 수집된 GPS 데이터를 로그로 출력
                            Log.d(TAG, "GPS 데이터 수집: " + gpsData.toString());
                        } else {
                            // 위치 데이터가 없는 경우 사용자에게 알림을 표시
                            Toast.makeText(activity, "GPS 데이터를 수집할 수 없습니다.", Toast.LENGTH_SHORT).show();
                            // 위치 데이터 수집 실패를 로그로 기록
                            Log.e(TAG, "GPS 데이터 수집 실패");
                        }
                    });
        } else {
            // 위치 권한이 없는 경우 권한을 요청
            requestLocationPermission();
        }
    }
}
