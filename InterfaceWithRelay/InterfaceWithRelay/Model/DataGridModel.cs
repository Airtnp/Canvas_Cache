using System.Collections.ObjectModel;

namespace InterfaceWithRelay.Model
{
    public class DataGridModel: IModel
    {
        public ObservableCollection<CourseFolderInfo> courseList;

        public DataGridModel()
        {
            courseList = new ObservableCollection<CourseFolderInfo>();
        }
    }
}
