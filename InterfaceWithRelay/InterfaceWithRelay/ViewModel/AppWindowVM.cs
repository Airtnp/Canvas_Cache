using InterfaceWithRelay.Model;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows.Data;

namespace InterfaceWithRelay.ViewModel
{
    public partial class AppWindowVM: NotifyPropertyChanged, IViewModel
    {
        #region MVVM model communication

        /// <summary>
        /// Reference to the views. 
        /// Do not use it anywhere before the initialization of windows.
        /// </summary>

        internal AppWindow appWindow;
        internal ICollectionView fileDataGridHelper;

        internal IdentityInfo identityModel = new IdentityInfo();
        internal DataGridModel dataGridModel = new DataGridModel();
        internal SettingsModel settingsModelReturned = new SettingsModel();

        #endregion

        #region Properties

        public string LoginName
        {
            get { return identityModel.CurrentUser.Name; }
            set { base.SetProperty(ref identityModel.CurrentUser.Name, value); }
        }

        public bool IsLoggedIn
        {
            get { return identityModel.CurrentUserLoggedIn; }
            set { base.SetProperty(ref identityModel.CurrentUserLoggedIn, value); }
        }

        public ObservableCollection<CourseFolderInfo> CourseList
        {
            get { return dataGridModel.courseList; }
            set { dataGridModel.courseList = value; }
        }

        public CourseFolderInfo SelectedCourse
        {
            get { return CourseList[selectedCourseIdx]; }
        }

        private int selectedCourseIdx;
        public int SelectedCourseIdx
        {
            get { return selectedCourseIdx; }
            set {
                base.SetProperty(ref selectedCourseIdx, value);
                base.OnPropertyChanged("SelectedCourse");
            }
        }

        #endregion

        #region Constructor

        public AppWindowVM(AppWindow window)
        {
            appWindow = window;
            fileDataGridHelper = CollectionViewSource.GetDefaultView(window.fileDataGrid.ItemsSource);
            SettingsButtonCommand = new RelayCommand(settingsButton_Execute);

#if DEBUG
            dataGridModel = FileLocalDummyReader.ReadModel(@"D:\SJTU\Sophomore S1");
#endif
        }

        #endregion

        #region setting button command

        public RelayCommand SettingsButtonCommand { get; private set; }

        private void settingsButton_Execute()
        {
            SettingsWindow window = new SettingsWindow(this);
            SettingsWindowVM windowVM = window.ObtainViewModel();
            /// Show window and wait for return.
            window.ShowDialog();
            /// After return, acquire the setting data as setting model.
            settingsModelReturned = windowVM.settingsModel;
        }

        #endregion
    }

    #region value converter

    [ValueConversion(typeof(bool), typeof(string))]
    public class LocationConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            bool local = (bool)value;
            if (local)
                return "Local";
            else
                return "Canvas";
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            string strPos = (string)value;
            if (strPos == "Local")
                return true;
            else if (strPos == "Canvas")
                return false;
            else throw new ArgumentException("Inputed file location not 'Local' or 'Canvas'.");
        }
    }

    #endregion
}
