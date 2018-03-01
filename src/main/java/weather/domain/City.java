package weather.domain;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.Transient;

@Embeddable
public class City {

    @Column(length = 255)
    private String name;
    private double longitude;
    private double latitude;

    @Transient
    private int openWeatherMapId;

    public City() {
    }

    public City(String name, double longitude, double latitude) {
        this.name = name;
        this.longitude = longitude;
        this.latitude = latitude;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public int getOpenWeatherMapId() {
        return openWeatherMapId;
    }

    public void setOpenWeatherMapId(int openWeatherMapId) {
        this.openWeatherMapId = openWeatherMapId;
    }
}
