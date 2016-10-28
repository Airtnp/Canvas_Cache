using InterfaceWithRelay.Model;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows;

namespace InterfaceWithRelay.ViewModel
{
    class LoginPageVM : NotifyPropertyChanged, IViewModel
    {
        #region MVVM model communication

        /// <summary>
        /// Reference to the views. 
        /// Do not use it anywhere before the initialization of windows.
        /// </summary>

        internal Window loginWindow;
        internal LoginPage loginPage;

        private IdentityInfo identityModel = new IdentityInfo();

        #endregion

        #region Properties

        public string LoginName
        {
            get { return identityModel.CurrentUser.Name; }
            set { base.SetProperty(ref identityModel.CurrentUser.Name, value); }
        }

        public string LoginPassword
        {
            get { return identityModel.CurrentUser.Password; }
            set { base.SetProperty(ref identityModel.CurrentUser.Password, value); }
        }

        public bool IsLoggedIn
        {
            get { return identityModel.CurrentUserLoggedIn; }
            set { base.SetProperty(ref identityModel.CurrentUserLoggedIn, value); }
        }

        public List<User> UserList
        {
            get { return identityModel.UserList; }
            private set { identityModel.UserList = value; }
        }

        #endregion

        #region Constructor

        public LoginPageVM(Window window)
        {
            loginWindow = window;
            loginPage = window.Content as LoginPage;

            LoginButtonCommand = new RelayCommand(loginButton_Execute, loginButton_CanExecute);
        }

        #endregion

        #region login button command

        public RelayCommand LoginButtonCommand { get; set; }

        private async void loginButton_Execute()
        {
            loginPage.progressBar.Start();
            await Task.Run(() =>
            {
                /// Fix this!
                System.Threading.Thread.Sleep(3000);

                IsLoggedIn = tryLoginFromVM();
#if DEBUG
                Console.WriteLine("Logged In!");
#endif
            });
            loginPage.progressBar.Stop();
            switchWindow();
        }

        private bool loginButton_CanExecute()
        {
            return (!string.IsNullOrEmpty(LoginName) && !string.IsNullOrEmpty(LoginPassword));
        }

        #endregion

        #region Login operation

        private bool tryLoginFromVM()
        {
            /// Fix this!
            return true;
        }
        #endregion

        private void switchWindow()
        {
            AppWindow appWindow = new AppWindow();
            (appWindow.DataContext as AppWindowVM).identityModel = identityModel;
            appWindow.Show();
            loginWindow.Close();
        }
    }
}
