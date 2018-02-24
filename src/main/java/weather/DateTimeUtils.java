package weather;

import org.joda.time.DateTime;
import org.springframework.stereotype.Service;

@Service
public class DateTimeUtils {

    public DateTime truncateToHour(DateTime dt) {
        return dt.hourOfDay().roundFloorCopy();
    }

}
