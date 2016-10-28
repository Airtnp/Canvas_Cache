using InterfaceWithRelay.Model;
using System.Collections.ObjectModel;
using System.Windows;

namespace InterfaceWithRelay.ViewModel
{
    public class AppWindowVM: NotifyPropertyChanged, IViewModel
    {
        #region MVVM model communication

        /// <summary>
        /// Reference to the views. 
        /// Do not use it anywhere before the initialization of windows.
        /// </summary>

        internal Window appWindow;

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

        #endregion

        #region Constructor

        public AppWindowVM(Window window)
        {
            appWindow = window;

            SettingsButtonCommand = new RelayCommand(settingsButton_Execute);
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
}
