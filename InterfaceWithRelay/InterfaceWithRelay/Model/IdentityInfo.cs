using System.Collections.Generic;

namespace InterfaceWithRelay.Model
{
    struct User
    {
        public string Name;
        public string Password;
    }

    /// <summary>
    /// Model class containing user info (list).
    /// Single instance of this class (together with other model classes) are created in App.xaml.
    /// </summary>
    class IdentityInfo: IModel
    {
        public User CurrentUser;

        public bool CurrentUserLoggedIn = false;

        public List<User> UserList;
    }

    class UserListIO
    {
        public string UserDataBaseLoc;

        public UserListIO(string dataLocation)
        {
            UserDataBaseLoc = dataLocation;
        }

        public async void SyncListWithLocal(List<User> userList)
        {

        }
    }
}
