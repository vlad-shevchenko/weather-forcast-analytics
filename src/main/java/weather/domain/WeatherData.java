package weather.domain;

import javax.persistence.Embeddable;

@Embeddable
public class WeatherData {

    private double temperature;
    private double humidity;
    private double windDirection;
    private double windSpeed;

    private WeatherData() {
    }

    public WeatherData(double temperature, double humidity, double windDirection, double windSpeed) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.windDirection = windDirection;
        this.windSpeed = windSpeed;
    }

    public double getTemperature() {
        return temperature;
    }

    public void setTemperature(double temperature) {
        this.temperature = temperature;
    }

    public double getHumidity() {
        return humidity;
    }

    public void setHumidity(double humidity) {
        this.humidity = humidity;
    }

    public double getWindDirection() {
        return windDirection;
    }

    public void setWindDirection(double windDirection) {
        this.windDirection = windDirection;
    }

    public double getWindSpeed() {
        return windSpeed;
    }

    public void setWindSpeed(double windSpeed) {
        this.windSpeed = windSpeed;
    }
}
