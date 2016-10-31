using System.IO;
using System.Collections.Generic;

namespace InterfaceWithRelay.Model
{
    public static class FileLocalDummyReader
    {
        public static DataGridModel ReadModel(string rootPath)
        {
            var ret = new DataGridModel();

            List<string> courseFolderList = new List<string>(
                Directory.GetDirectories(rootPath));

            foreach (string courseFolderPath in courseFolderList)
            {
                string[] nodes = courseFolderPath.Split(Path.DirectorySeparatorChar);
                string courseFolder = nodes[nodes.Length - 1];
                CourseFolderInfo thisCourse = new CourseFolderInfo() { CourseName = courseFolder };

                List<string> fileList = new List<string>(
                    Directory.GetFiles(courseFolderPath));
                foreach (string filePath in fileList)
                {
                    thisCourse.FileList.Add(new CanvasFileInfo(filePath, false));
                    thisCourse.FileList.Add(new CanvasFileInfo(filePath, true));
                }

                ret.courseList.Add(thisCourse);
            }

            return ret;
        }
    }
}