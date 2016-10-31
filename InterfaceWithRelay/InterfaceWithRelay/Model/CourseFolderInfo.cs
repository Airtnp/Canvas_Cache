using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterfaceWithRelay.Model
{
    public class CourseFolderInfo
    {
        public string CourseName { get; set; }
        public string FolderPath { get; set; }

        private ObservableCollection<CanvasFileInfo> fileList = new ObservableCollection<CanvasFileInfo>();
        public ObservableCollection<CanvasFileInfo> FileList
        {
            get { return fileList; }
            private set { fileList = value; }
        }
        
        public void UpdateLocalFileList()
        {

        }
    }
}
