package weather.domain;

import org.hibernate.annotations.Type;
import org.joda.time.DateTime;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import java.io.Serializable;

@Embeddable
public class WeatherKey implements Serializable {

    @Column(length = 50)
    private String wdpName;
    @Column(length = 50)
    private String city;
    @Type(type="org.jadira.usertype.dateandtime.joda.PersistentDateTime")
    private DateTime dateTime;

    private WeatherKey() {
    }

    public WeatherKey(String wdpName, String city, DateTime dateTime) {
        this.wdpName = wdpName;
        this.city = city;
        this.dateTime = dateTime;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        WeatherKey that = (WeatherKey) o;

        if (!wdpName.equals(that.wdpName)) return false;
        if (!city.equals(that.city)) return false;
        return dateTime.equals(that.dateTime);
    }

    @Override
    public int hashCode() {
        int result = wdpName.hashCode();
        result = 31 * result + city.hashCode();
        result = 31 * result + dateTime.hashCode();
        return result;
    }

    public String getWdpName() {
        return wdpName;
    }

    public void setWdpName(String wdpName) {
        this.wdpName = wdpName;
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
