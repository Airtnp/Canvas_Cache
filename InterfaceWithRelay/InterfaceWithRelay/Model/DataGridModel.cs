using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterfaceWithRelay.Model
{
    class DataGridModel: IModel
    {
        public ObservableCollection<CourseFolderInfo> courseList;

        public DataGridModel()
        {
            courseList = new ObservableCollection<CourseFolderInfo>();
            courseList.Add(new CourseFolderInfo() { CourseName = "VV286", FolderPath = "null"});
        }
    }
}
