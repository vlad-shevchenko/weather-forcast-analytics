package weather.domain;

import org.joda.time.DateTime;

import javax.persistence.Embeddable;
import java.io.Serializable;

@Embeddable
public class WeatherKey implements Serializable {

    private String city;
    private DateTime dateTime;

    private WeatherKey() {
    }

    public WeatherKey(String city, DateTime dateTime) {
        this.city = city;
        this.dateTime = dateTime;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        WeatherKey that = (WeatherKey) o;

        if (!city.equals(that.city)) return false;
        return dateTime.equals(that.dateTime);
    }

    @Override
    public int hashCode() {
        int result = city.hashCode();
        result = 31 * result + dateTime.hashCode();
        return result;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public DateTime getDateTime() {
        return dateTime;
    }

    public void setDateTime(DateTime dateTime) {
        this.dateTime = dateTime;
    }
}
