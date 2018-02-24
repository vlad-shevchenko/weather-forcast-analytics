package weather.domain;

import org.hibernate.annotations.Type;
import org.joda.time.DateTime;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import java.io.Serializable;

@Embeddable
public class ForecastKey implements Serializable {

    @Column(length = 50)
    private String wdpName;
    @Column(length = 50)
    private String city;
    @Type(type="org.jadira.usertype.dateandtime.joda.PersistentDateTime")
    private DateTime targetTime;
    @Type(type="org.jadira.usertype.dateandtime.joda.PersistentDateTime")
    private DateTime forecastCreationTime;

    private ForecastKey() {
    }

    public ForecastKey(String wdpName, String city, DateTime targetTime, DateTime forecastCreationTime) {
        this.wdpName = wdpName;
        this.city = city;
        this.targetTime = targetTime;
        this.forecastCreationTime = forecastCreationTime;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        ForecastKey that = (ForecastKey) o;

        if (!wdpName.equals(that.wdpName)) return false;
        if (!city.equals(that.city)) return false;
        if (!targetTime.equals(that.targetTime)) return false;
        return forecastCreationTime.equals(that.forecastCreationTime);
    }

    @Override
    public int hashCode() {
        int result = wdpName.hashCode();
        result = 31 * result + city.hashCode();
        result = 31 * result + targetTime.hashCode();
        result = 31 * result + forecastCreationTime.hashCode();
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

    public DateTime getTargetTime() {
        return targetTime;
    }

    public void setTargetTime(DateTime targetTime) {
        this.targetTime = targetTime;
    }

    public DateTime getForecastCreationTime() {
        return forecastCreationTime;
    }

    public void setForecastCreationTime(DateTime forecastCreationTime) {
        this.forecastCreationTime = forecastCreationTime;
    }
}
